package logx

import (
	"context"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

const ctxKeyReqId = "request_id"

type InnerLogger struct {
	zapLogger *zap.Logger
	ctx       context.Context
	fields    []interface{}
}

func NewInnerLogger() *InnerLogger {
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

func (l *InnerLogger) Debugf(msg string, args ...interface{}) {
	fields := l.buildFields()
	if len(fields) > 0 {
		l.zapLogger.Sugar().With(fields...).Debugf(msg, args...)
	} else {
		l.zapLogger.Sugar().Debugf(msg, args...)
	}
}

func (l *InnerLogger) Infof(msg string, args ...interface{}) {
	fields := l.buildFields()
	if len(fields) > 0 {
		l.zapLogger.Sugar().With(fields...).Infof(msg, args...)
	} else {
		l.zapLogger.Sugar().Infof(msg, args...)
	}
}

func (l *InnerLogger) Warnf(msg string, args ...interface{}) {
	fields := l.buildFields()
	if len(fields) > 0 {
		l.zapLogger.Sugar().With(fields...).Warnf(msg, args...)
	} else {
		l.zapLogger.Sugar().Warnf(msg, args...)
	}
}

func (l *InnerLogger) Errorf(msg string, args ...interface{}) {
	//l.zapLogger.Sugar().With(l.buildFields()).Errorf(msg, args...)
	fields := l.buildFields()
	if len(fields) > 0 {
		l.zapLogger.Sugar().With(fields...).Errorf(msg, args...)
	} else {
		l.zapLogger.Sugar().Errorf(msg, args...)
	}
}

func (l *InnerLogger) Fatalf(msg string, args ...interface{}) {
	//l.zapLogger.Sugar().With(l.buildFields()).Panicf(msg, args...)
	fields := l.buildFields()
	if len(fields) > 0 {
		l.zapLogger.Sugar().With(fields...).Panicf(msg, args...)
	} else {
		l.zapLogger.Sugar().Panicf(msg, args...)
	}
}
