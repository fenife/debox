package logx

// LogOption 定义一个选项结构体
type LogOptions struct {
	logFile       string // 完整的log文件路径
	level         Level  // log级别
	isEncodeJson  bool   // 是否用Json格式记录日志
	isEncodePlain bool   // plain格式记录日志，跟isEncodeJson只能二选一
	addCaller     bool   // 是否需要打印调用者信息
	callerCount   int    // 打印多少个调用者信息
	addGoId       bool
}

func NewDefaultLogOptions() *LogOptions {
	return &LogOptions{
		logFile:       "",
		level:         InfoLevel,
		isEncodeJson:  false,
		isEncodePlain: true,
		addCaller:     false,
		callerCount:   1,
		addGoId:       false,
	}
}

// OptFunc 定义一个选项函数类型
type OptFunc func(*LogOptions)

func WithLogFile(logFile string) OptFunc {
	return func(o *LogOptions) {
		o.logFile = logFile
	}
}

func WithLevel(lvl Level) OptFunc {
	return func(o *LogOptions) {
		o.level = lvl
	}
}

func WithEncodeJson() OptFunc {
	return func(o *LogOptions) {
		o.isEncodeJson = true
	}
}

func WithEncodePlain() OptFunc {
	return func(o *LogOptions) {
		o.isEncodePlain = true
	}
}

func WithCaller() OptFunc {
	return func(o *LogOptions) {
		o.addCaller = true
	}
}

func WithCallerCount(count int) OptFunc {
	return func(o *LogOptions) {
		o.callerCount = count
	}
}

func WithGoid() OptFunc {
	return func(o *LogOptions) {
		o.addGoId = true
	}
}
