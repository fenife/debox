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

type InnerLogger struct {
	zapLogger *zap.Logger
	ctx       context.Context
	fields    []interface{}
}

func NewInnerLogger(logFile string) *InnerLogger {
	writers := []zapcore.WriteSyncer{zapcore.AddSync(os.Stdout)}
	if logFile != "" {
		fileWriter := zapcore.AddSync(&lumberjack.Logger{
			Filename:   logFile, // 文件位置
			MaxSize:    100,     // 日志文件的最大大小(MB为单位)
			MaxAge:     10,      // 保留旧文件的最大天数
			MaxBackups: 10,      // 保留旧文件的最大个数
			Compress:   false,   // 是否压缩/归档旧文件
		})
		writers = append(writers, zapcore.AddSync(fileWriter))
	}

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

	core := zapcore.NewCore(
		// zapcore.NewJSONEncoder(encodeConfig),
		zapcore.NewConsoleEncoder(encodeConfig),
		zapcore.NewMultiWriteSyncer(writers...),
		zap.DebugLevel,
	)
	// zapLogger := zap.New(core, zap.AddCaller(), zap.AddCallerSkip(2))
	zapLogger := zap.New(core)
	return &InnerLogger{
		zapLogger: zapLogger,
		fields:    make([]interface{}, 0),
	}
}

func newInnerLogger() *InnerLogger {
	config := zap.NewProductionConfig()
	config.EncoderConfig.EncodeTime = zapcore.TimeEncoderOfLayout("2006-01-02 15:05:05.000")
	config.Level = zap.NewAtomicLevelAt(zap.DebugLevel)
	config.DisableStacktrace = true

	// log function name
	//config.EncoderConfig.FunctionKey = "func"
	opts := []zap.Option{
		zap.AddCallerSkip(1),
		zap.AddCaller(),
	}

	zapLogger, err := config.Build(opts...)
	if err != nil {
		panic(err)
	}

	return &InnerLogger{
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

func (l *InnerLogger) buildFields() []interface{} {
	if l.ctx != nil {
		if val := l.ctx.Value(ctxKeyReqId); val != nil {
			l.fields = append(l.fields, ctxKeyReqId, val)
		}
	}
	return l.fields
}

func (l *InnerLogger) buildExtras(msg string, args ...interface{}) (string, []interface{}) {
	callerStackStr := GetCallerStackStr(4, 7)
	prefix := fmt.Sprintf("[%s] -- ", callerStackStr)
	if msg == "" && len(args) != 0 {
		args = append([]interface{}{prefix}, args...)
	} else {
		msg = prefix + msg
	}
	return msg, args
}

func (l *InnerLogger) Logf(lvl Level, msg string, args ...interface{}) {
	zapLevel := toZapLevel(lvl)
	fields := l.buildFields()
	msg, args = l.buildExtras(msg, args...)
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
