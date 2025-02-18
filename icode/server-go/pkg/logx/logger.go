package logx

import (
	"context"
	"fmt"
	"os"

	"github.com/natefinch/lumberjack"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

const ctxKeyReqId = "request_id"
const ctxKeyTraceId = "trace_id"

type InnerLogger struct {
	opt       *LogOptions
	zapLogger *zap.Logger
	ctx       context.Context
	fields    []interface{}
}

func (l *InnerLogger) NewWithCtx(ctx context.Context) *InnerLogger {
	return &InnerLogger{
		opt:       l.opt,
		zapLogger: l.zapLogger,
		ctx:       ctx,
		fields:    make([]interface{}, 0),
	}
}

func NewInnerLogger(opts ...OptFunc) *InnerLogger {
	opt := NewDefaultLogOptions()
	for _, optFunc := range opts {
		optFunc(opt)
	}
	writers := []zapcore.WriteSyncer{zapcore.AddSync(os.Stdout)}
	if opt.logFile != "" {
		fileWriter := zapcore.AddSync(&lumberjack.Logger{
			Filename:   opt.logFile, // 文件位置
			MaxSize:    100,         // 日志文件的最大大小(MB为单位)
			MaxAge:     10,          // 保留旧文件的最大天数
			MaxBackups: 10,          // 保留旧文件的最大个数
			Compress:   false,       // 是否压缩/归档旧文件
		})
		writers = append(writers, zapcore.AddSync(fileWriter))
	}
	multiWriter := zapcore.NewMultiWriteSyncer(writers...)

	encodeConfig := zapcore.EncoderConfig{
		TimeKey:        "ts",
		LevelKey:       "level",
		NameKey:        "logger",
		CallerKey:      "caller",
		FunctionKey:    zapcore.OmitKey,
		MessageKey:     "msg",
		StacktraceKey:  "stacktrace",
		LineEnding:     zapcore.DefaultLineEnding,
		EncodeLevel:    zapcore.LowercaseLevelEncoder,
		EncodeTime:     zapcore.TimeEncoderOfLayout("2006-01-02 15:05:05.000"),
		EncodeDuration: zapcore.SecondsDurationEncoder,
		EncodeCaller:   zapcore.ShortCallerEncoder,
	}

	zapLevel := toZapLevel(Level(opt.level))
	enc := zapcore.NewConsoleEncoder(encodeConfig)
	if opt.isEncodeJson {
		enc = zapcore.NewJSONEncoder(encodeConfig)
	}
	core := zapcore.NewCore(enc, multiWriter, zapLevel)
	zapLogger := zap.New(core)
	return &InnerLogger{
		opt:       opt,
		zapLogger: zapLogger,
		fields:    make([]interface{}, 0),
	}
}

func (l *InnerLogger) Ctx(ctx context.Context) Loggerx {
	l.ctx = ctx
	return l
}

func (l *InnerLogger) With(keyAndValues ...interface{}) Loggerx {
	l.fields = append(l.fields, keyAndValues...)
	return l
}

// 公共字段（一个logger的一次context中共用）
func (l *InnerLogger) buildFields() []interface{} {
	if l.ctx == nil {
		return l.fields
	}
	if val := l.ctx.Value(ctxKeyReqId); val != nil {
		l.fields = append(l.fields, ctxKeyReqId, val)
	}
	if val := l.ctx.Value(ctxKeyTraceId); val != nil {
		l.fields = append(l.fields, ctxKeyTraceId, val)
	}
	return l.fields
}

func (l *InnerLogger) Logf(lvl Level, msg string, args ...interface{}) {
	zapLevel := toZapLevel(lvl)
	fields := l.buildFields()

	// 加入caller，goid，trace_id 等信息
	callerStart := 3
	callerEnd := callerStart + l.opt.callerCount
	stackStr := GetCallerStackStr(callerStart, callerEnd)
	if l.opt.isEncodeJson {
		if l.opt.addCaller {
			fields = append(fields, "stack", stackStr)
		}
	} else {
		if l.opt.addCaller {
			prefix := fmt.Sprintf("[%s] -- ", stackStr)
			if msg == "" {
				args = append([]interface{}{prefix}, args...)
			} else {
				msg = prefix + msg
			}
		}
	}

	// 输出日志
	l.zapLogger.Sugar().With(fields...).Logf(zapLevel, msg, args...)
}

func (l *InnerLogger) Debugf(msg string, args ...interface{}) {
	l.Logf(DebugLevel, msg, args...)
}

func (l *InnerLogger) Infof(msg string, args ...interface{}) {
	l.Logf(InfoLevel, msg, args...)
}

func (l *InnerLogger) Warnf(msg string, args ...interface{}) {
	l.Logf(WarnLevel, msg, args...)
}

func (l *InnerLogger) Errorf(msg string, args ...interface{}) {
	l.Logf(ErrorLevel, msg, args...)
}

func (l *InnerLogger) Fatalf(msg string, args ...interface{}) {
	l.Logf(FatalLevel, msg, args...)
}
