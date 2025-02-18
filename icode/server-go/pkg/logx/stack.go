package logx

import (
	"bytes"
	"runtime"
	"strconv"
	"strings"

	"github.com/petermattis/goid"
)

type Stack struct {
	frames []runtime.Frame
}

func (stack *Stack) Format() string {
	if len(stack.frames) == 0 {
		return ""
	}
	formatStrings := make([]string, 0)
	// 倒序
	for i := len(stack.frames) - 1; i >= 0; i-- {
		frame := stack.frames[i]
		s := stack.formatFrame(frame)
		formatStrings = append(formatStrings, s)
	}
	// 正序
	// for _, frame := range stack.frames {
	// 	s := stack.formatFrame(frame)
	// 	formatStrings = append(formatStrings, s)
	// }
	return strings.Join(formatStrings, ", ")
}

func (stack *Stack) formatFrame(frame runtime.Frame) string {
	var buf bytes.Buffer
	buf.WriteString(stack.shortFileName(frame.File))
	buf.WriteByte(':')
	buf.WriteString(strconv.Itoa(frame.Line))
	buf.WriteByte(':')
	buf.WriteString(stack.shortFuncName(frame.Function))
	return buf.String()
}

func (stack *Stack) shortFileName(filename string) string {
	idx := strings.LastIndexByte(filename, '/')
	if idx == -1 {
		return filename
	}
	return filename[idx+1:]
}

func (stack *Stack) shortFuncName(funcname string) string {
	idx := strings.LastIndexByte(funcname, '.')
	if idx == -1 {
		return funcname
	}
	return funcname[idx+1:]
}

// GetCallerStack 获取指定范围的调用栈帧信息
func GetCallerStack(start, end int) *Stack {
	stack := &Stack{
		frames: nil,
	}
	var frames []runtime.Frame
	pcs := make([]uintptr, 10)
	// 跳过前 2 帧（runtime.Callers 和 GetCallerStack 本身）
	n := runtime.Callers(2, pcs)
	if n == 0 {
		return stack
	}

	framesInfo := runtime.CallersFrames(pcs[:n])
	frameIndex := 0
	for {
		frame, more := framesInfo.Next()
		if !more {
			break
		}
		if frameIndex >= start && frameIndex < end {
			frames = append(frames, frame)
		}
		frameIndex++
	}
	stack.frames = frames
	return stack
}

func GetCallerStackStr(start, end int) string {
	stack := GetCallerStack(start, end)
	s := stack.Format()
	return s
}

func GetGoid() int64 {
	return goid.Get()
}
