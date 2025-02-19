package logx

import (
	"context"

	"go.uber.org/zap/zapcore"
)

type Level string

const (
	DebugLevel Level = "debug"
	InfoLevel  Level = "info"
	WarnLevel  Level = "warn"
	ErrorLevel Level = "error"
	FatalLevel Level = "fatal"
)

func (lvl Level) toZapLevel() zapcore.Level {
	zapLevel := zapcore.InfoLevel
	switch lvl {
	case DebugLevel:
		zapLevel = zapcore.DebugLevel
	case InfoLevel:
		zapLevel = zapcore.InfoLevel
	case WarnLevel:
		zapLevel = zapcore.WarnLevel
	case ErrorLevel:
		zapLevel = zapcore.ErrorLevel
	case FatalLevel:
		zapLevel = zapcore.FatalLevel
	default:
		zapLevel = zapcore.InfoLevel
	}
	return zapLevel
}

func toZapLevel(lvl Level) zapcore.Level {
	return lvl.toZapLevel()
}

type Loggerx interface {
	Ctx(ctx context.Context) Loggerx
	With(keyAndValues ...interface{}) Loggerx
	Logf(lvl Level, msg string, args ...interface{})
	Debugf(msg string, args ...interface{})
	Infof(msg string, args ...interface{})
	Warnf(msg string, args ...interface{})
	Errorf(msg string, args ...interface{})
	Fatalf(msg string, args ...interface{})
}

var innerLogger *InnerLogger

func InitLogger(opts ...OptFunc) {
	innerLogger = NewInnerLogger(opts...)
}

func ctxLogger(ctx context.Context) Loggerx {
	newLogger := innerLogger.Clone(ctx)
	return newLogger
}

func emptyCtxLogger() Loggerx {
	return ctxLogger(context.Background())
}

func Ctx(ctx context.Context) Loggerx {
	return ctxLogger(ctx)
}

func With(keyAndValues ...interface{}) Loggerx {
	return emptyCtxLogger().With(keyAndValues...)
}

func Debugf(msg string, args ...interface{}) {
	emptyCtxLogger().Logf(DebugLevel, msg, args...)
}

func Infof(msg string, args ...interface{}) {
	emptyCtxLogger().Logf(InfoLevel, msg, args...)
}

func Warnf(msg string, args ...interface{}) {
	emptyCtxLogger().Logf(WarnLevel, msg, args...)
}

func Errorf(msg string, args ...interface{}) {
	emptyCtxLogger().Logf(ErrorLevel, msg, args...)
}

func Fatalf(msg string, args ...interface{}) {
	emptyCtxLogger().Logf(FatalLevel, msg, args...)
}

func init() {
	InitLogger(
		WithLevel(DebugLevel),
		// WithEncodeJson(),
		WithCaller(),
		WithCallerCount(3),
		WithGoid(),
	)
}
