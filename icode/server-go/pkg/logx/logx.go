package logx

import "context"

type Loggerx interface {
	Ctx(ctx context.Context) Loggerx
	With(keyAndValues ...interface{}) Loggerx
	Debugf(msg string, args ...interface{})
	Infof(msg string, args ...interface{})
	Warnf(msg string, args ...interface{})
	Errorf(msg string, args ...interface{})
	Fatalf(msg string, args ...interface{})
}

var innerLogger *InnerLogger

func InitLogger() {
	innerLogger = NewInnerLogger()
}

func Ctx(ctx context.Context) Loggerx {
	l := &InnerLogger{
		zapLogger: innerLogger.zapLogger,
		ctx:       ctx,
		fields:    make([]interface{}, 0),
	}
	return l
}

func Debugf(msg string, args ...interface{}) {
	innerLogger.Debugf(msg, args...)
}

func Infof(msg string, args ...interface{}) {
	innerLogger.Infof(msg, args...)
}

func Warnf(msg string, args ...interface{}) {
	innerLogger.Warnf(msg, args...)
}

func Errorf(msg string, args ...interface{}) {
	innerLogger.Errorf(msg, args...)
}

func Fatalf(msg string, args ...interface{}) {
	innerLogger.Fatalf(msg, args...)
}

func init() {
	InitLogger()
}
