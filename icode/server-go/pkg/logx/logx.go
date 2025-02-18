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

func toZapLevel(lvl Level) zapcore.Level {
	levelMaps := map[Level]zapcore.Level{
		DebugLevel: zapcore.DebugLevel,
		InfoLevel:  zapcore.InfoLevel,
		WarnLevel:  zapcore.WarnLevel,
		ErrorLevel: zapcore.ErrorLevel,
		FatalLevel: zapcore.FatalLevel,
	}
	zapLevel := zapcore.InfoLevel
	level, ok := levelMaps[lvl]
	if ok {
		zapLevel = level
	}
	return zapLevel
}

func InitLogger(opts ...OptFunc) {
	innerLogger = NewInnerLogger(opts...)
}

func Ctx(ctx context.Context) Loggerx {
	newLogger := innerLogger.NewWithCtx(ctx)
	return newLogger
}

func EmptyCtx() Loggerx {
	newLogger := innerLogger.NewWithCtx(context.Background())
	return newLogger
}

func With(keyAndValues ...interface{}) Loggerx {
	return Ctx(context.Background()).With(keyAndValues...)
}

func Debugf(msg string, args ...interface{}) {
	EmptyCtx().Logf(DebugLevel, msg, args...)
}

func Infof(msg string, args ...interface{}) {
	EmptyCtx().Logf(InfoLevel, msg, args...)
}

func Warnf(msg string, args ...interface{}) {
	EmptyCtx().Logf(WarnLevel, msg, args...)
}

func Errorf(msg string, args ...interface{}) {
	EmptyCtx().Logf(ErrorLevel, msg, args...)
}

func Fatalf(msg string, args ...interface{}) {
	EmptyCtx().Logf(FatalLevel, msg, args...)
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
