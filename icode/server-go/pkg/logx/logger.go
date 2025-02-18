package logx

import (
	"context"
	"fmt"
	"os"
	"strings"

	"github.com/natefinch/lumberjack"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

const keyReqId = "request_id"
const keyTraceId = "trace_id"
const keyGoid = "goid"
const keyStack = "stack"

type InnerLogger struct {
	opt       *LogOptions
	zapLogger *zap.Logger
	ctx       context.Context
	fields    []interface{}
	extras    map[string]interface{}
}

// var prefixKeyOrders = []string{keyGoid, keyStack, keyReqId, keyTraceId}
var prefixKeyOrders = []string{keyGoid, keyReqId, keyTraceId, keyStack}

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

	zapLevel := toZapLevel(opt.level)
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
		extras:    make(map[string]interface{}, 0),
	}
}

func (l *InnerLogger) NewWithCtx(ctx context.Context) *InnerLogger {
	return &InnerLogger{
		opt:       l.opt,
		zapLogger: l.zapLogger,
		ctx:       ctx,
		fields:    make([]interface{}, 0),
		extras:    make(map[string]interface{}, 0),
	}
}

// 公共字段（一个logger的一次context中共用）
func (l *InnerLogger) buildExtras() {
	if l.ctx != nil {
		if val := l.ctx.Value(keyReqId); val != nil {
			l.extras[keyReqId] = val
		}
		if val := l.ctx.Value(keyTraceId); val != nil {
			l.extras[keyTraceId] = val
		}
	}
	if l.opt.addGoId {
		l.extras[keyGoid] = GetGoid()
	}
	if l.opt.addCaller {
		callerStart := 4
		callerEnd := callerStart + l.opt.callerCount
		l.extras[keyStack] = GetCallerStackStr(callerStart, callerEnd)
	}
}

func (l *InnerLogger) extraToSlices(withKey bool) []interface{} {
	fields := make([]interface{}, 0)
	if len(l.extras) == 0 {
		return fields
	}
	for _, k := range prefixKeyOrders {
		if v, ok := l.extras[k]; ok {
			if withKey {
				fields = append(fields, k, v)
			} else {
				fields = append(fields, v)
			}
		}
	}
	return fields
}

// 构造log前缀，类似："[6] [logx_test.go:10:TestLog] -- "
func (l *InnerLogger) extraToPrefixStr() string {
	extras := l.extraToSlices(false)
	prefixFields := make([]string, 0)
	for _, field := range extras {
		prefixFields = append(prefixFields, fmt.Sprintf("[%v]", field))
	}
	prefixFields = append(prefixFields, "-- ")
	prefixStr := strings.Join(prefixFields, " ")
	return prefixStr
}

func (l *InnerLogger) logJson(lvl Level, msg string, args ...interface{}) {
	zapLevel := toZapLevel(lvl)
	extras := l.extraToSlices(true)
	fields := append(extras, l.fields...)
	l.zapLogger.Sugar().With(fields...).Logf(zapLevel, msg, args...)
}

func (l *InnerLogger) log(lvl Level, args ...interface{}) {
	zapLevel := toZapLevel(lvl)
	prefixStr := l.extraToPrefixStr()
	newArgs := append([]interface{}{prefixStr}, args...)
	l.zapLogger.Sugar().With(l.fields...).Log(zapLevel, newArgs...)
}

func (l *InnerLogger) logf(lvl Level, msg string, args ...interface{}) {
	zapLevel := toZapLevel(lvl)
	prefixStr := l.extraToPrefixStr()
	msg = prefixStr + msg
	l.zapLogger.Sugar().With(l.fields...).Logf(zapLevel, msg, args...)
}

func (l *InnerLogger) Ctx(ctx context.Context) Loggerx {
	l.ctx = ctx
	return l
}

func (l *InnerLogger) With(keyAndValues ...interface{}) Loggerx {
	l.fields = append(l.fields, keyAndValues...)
	return l
}

func (l *InnerLogger) Logf(lvl Level, msg string, args ...interface{}) {
	l.buildExtras()
	if l.opt.isEncodeJson {
		l.logJson(lvl, msg, args...)
	} else if msg == "" {
		l.log(lvl, args...)
	} else {
		l.logf(lvl, msg, args...)
	}
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
