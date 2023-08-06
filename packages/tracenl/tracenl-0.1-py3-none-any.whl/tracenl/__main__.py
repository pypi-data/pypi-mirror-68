import argparse
import ctypes
import textwrap
from pprint import pformat

from pyroute2.netlink.nl80211 import nl80211cmd

from ptrace.debugger import (
    PtraceDebugger,
    ProcessExit,
    ProcessSignal,
    NewProcessEvent,
    ProcessExecution,
)
from ptrace.debugger.child import createChild
from ptrace.ctypes_tools import formatAddress

from ptrace.func_call import FunctionCallOptions

c_socklen_t = ctypes.c_uint


class c_sockaddr_nl(ctypes.Structure):
    _fields_ = [
        ("nl_family", ctypes.c_uint16),
        ("nl_pad", ctypes.c_uint16),
        ("nl_pid", ctypes.c_uint32),
        ("nl_groups", ctypes.c_uint32),
    ]


class c_iovec(ctypes.Structure):
    _fields_ = [("iov_base", ctypes.c_void_p), ("iov_len", ctypes.c_size_t)]


class c_msghdr(ctypes.Structure):
    _fields_ = [
        ("msg_name", ctypes.c_void_p),
        ("msg_namelen", c_socklen_t),
        ("msg_iov", ctypes.c_void_p),
        ("msg_iovlen", ctypes.c_size_t),
        ("msg_control", ctypes.c_void_p),
        ("msg_controllen", ctypes.c_size_t),
        ("msg_flag", ctypes.c_int),
    ]


def decode_netlink(buf):
    nl_msg = nl80211cmd(buf)
    nl_msg.decode()
    print(textwrap.indent(pformat(nl_msg), "  "))


def handle_sendmsg(syscall):
    process = syscall.process
    msg_ptr = syscall["msg"].value
    msg_hdr = process.readStruct(msg_ptr, c_msghdr)

    # read structaddr family
    nl_family = None
    if msg_hdr.msg_name:
        msg_name = process.readStruct(msg_hdr.msg_name, c_sockaddr_nl)
        nl_family = msg_name.nl_family

    # netlink only
    if nl_family != 16:
        return

    # read iov scatter/gather array
    msg_chunks = []
    for ii in range(msg_hdr.msg_iovlen):
        iovec_addr = msg_hdr.msg_iov + (ii * ctypes.sizeof(ctypes.c_void_p))
        iovec = process.readStruct(iovec_addr, c_iovec)
        msg_chunks.append(process.readBytes(iovec.iov_base, iovec.iov_len))

    msg = b"".join(msg_chunks)
    decode_netlink(msg)


def handle_sendto(syscall):
    process = syscall.process

    p_sockaddr = syscall["dest_addr"].value
    if not p_sockaddr:
        return

    sockaddr = process.readStruct(p_sockaddr, c_sockaddr_nl)
    if sockaddr.nl_family != 16:
        return

    p_msg = syscall["buf"].value
    if not p_msg:
        return

    msg = process.readBytes(p_msg, syscall["len"].value)
    decode_netlink(msg)


def handle_recvfrom(syscall):
    process = syscall.process

    p_msg = syscall["buf"].value
    if not p_msg:
        return

    msg = process.readBytes(p_msg, syscall["len"].value)
    decode_netlink(msg)


def display_syscall(syscall, show_pid=True, show_ip=False):
    if syscall.result is None:
        return

    text = syscall.format()
    if syscall.result is not None:
        text = "%-40s = %s" % (text, syscall.result_text)
    prefix = []
    if show_pid:
        prefix.append("[%s]" % syscall.process.pid)
    if show_ip:
        prefix.append("[%s]" % formatAddress(syscall.instr_pointer))
    if prefix:
        text = "".join(prefix) + " " + text
    print(text)

    if syscall.name in ("sendmsg", "recvmsg"):
        handle_sendmsg(syscall)

    elif syscall.name in ("sendto"):
        handle_sendto(syscall)

    elif syscall.name in ("recvfrom"):
        handle_recvfrom(syscall)


def syscall_filter(syscall):
    return syscall.name not in ("sendmsg", "recvmsg", "sendto", "recvfrom")


def prepare_process(process):
    process.syscall_state.ignore_callback = syscall_filter


def handle_exit(event):
    print("*** %s ***" % event)


def handle_signal(event):
    event.display()
    event.process.syscall(event.signum)


def handle_new_process(event):
    process = event.process
    print("*** New process %s ***" % process.pid)

    prepare_process(process)
    process.syscall()
    process.parent.syscall()


def handle_exec(event):
    process = event.process
    print("*** Process %s execution ***" % process.pid)
    process.syscall()


def handle_syscall(event, display_options):
    process = event.process
    state = process.syscall_state

    syscall = state.event(display_options)
    if syscall:
        # if syscall and (syscall.result is not None or self.options.enter):
        display_syscall(syscall)

    process.syscall()


def watch_syscalls(dbg):
    syscall_options = FunctionCallOptions(
        write_types=False,
        write_argname=True,
        string_max_length=300,
        replace_socketcall=True,
        write_address=False,
        max_array_count=20,
    )
    syscall_options.instr_pointer = False

    # tell all processes to break at the next syscall
    for process in dbg:
        prepare_process(process)
        process.syscall()

    while True:
        if not dbg:
            break

        # wait for next syscall event
        try:
            event = dbg.waitSyscall()
        except ProcessExit as event:
            handle_exit(event)
            continue
        except ProcessSignal as event:
            handle_signal(event)
            continue
        except NewProcessEvent as event:
            handle_new_process(event)
            continue
        except ProcessExecution as event:
            handle_exec(event)
            continue

        # process syscall enter or exit
        handle_syscall(event, syscall_options)


def start_trace(cmd):
    new_pid = createChild(cmd, no_stdout=False)

    debugger = PtraceDebugger()
    debugger.traceFork()
    debugger.traceExec()
    debugger.addProcess(new_pid, is_attached=True)

    return debugger


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="+")

    opts = ap.parse_args()

    debugger = start_trace(opts.cmd)
    watch_syscalls(debugger)
