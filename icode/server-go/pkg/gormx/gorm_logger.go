package gormx

import (
	"context"
	"errors"
	"fmt"
	"gorm.io/gorm"
	glogger "gorm.io/gorm/logger"
	"gorm.io/gorm/utils"
	"server-go/pkg/logx"
	"strings"
	"time"
)

type gormLogger struct {
	glogger.Writer
	glogger.Config
}

func NewGormLogger() glogger.Interface {
	return &gormLogger{
		Writer: NewGormWriter(),
		Config: glogger.Config{
			SlowThreshold:             5 * time.Second, // Slow SQL threshold
			LogLevel:                  glogger.Info,    // Log level
			IgnoreRecordNotFoundError: true,            // Ignore ErrRecordNotFound error for logger
			ParameterizedQueries:      false,           // Don't include params in the SQL log
		},
	}
}

func (l *gormLogger) LogMode(level glogger.LogLevel) glogger.Interface {
	newLogger := *l
	newLogger.LogLevel = level
	return &newLogger
}

func (l *gormLogger) Info(ctx context.Context, msg string, data ...interface{}) {
	if l.LogLevel >= glogger.Info {
		logx.Ctx(ctx).With("file", utils.FileWithLineNum()).Infof(msg, data...)
	}
}

func (l *gormLogger) Warn(ctx context.Context, msg string, data ...interface{}) {
	if l.LogLevel >= glogger.Warn {
		logx.Ctx(ctx).With("file", utils.FileWithLineNum()).Warnf(msg, data...)
	}
}

func (l *gormLogger) Error(ctx context.Context, msg string, data ...interface{}) {
	if l.LogLevel >= glogger.Error {
		logx.Ctx(ctx).With("file", utils.FileWithLineNum()).Errorf(msg, data...)
	}
}

func (l *gormLogger) Trace(ctx context.Context, begin time.Time, fc func() (sql string, rowsAffected int64), err error) {
	if l.LogLevel <= glogger.Silent {
		return
	}

	sql, rows := fc() // 执行sql
	var rowsLogVal interface{}
	if rows == -1 {
		rowsLogVal = "-"
	} else {
		rowsLogVal = rows
	}

	elapsed := time.Since(begin)
	internal := elapsed.Milliseconds() // 毫秒

	lgr := logx.Ctx(ctx).With("file", getShortFileLine(utils.FileWithLineNum()), "internal", internal, "rows", rowsLogVal, "sql", sql)

	switch {
	case err != nil && l.LogLevel >= glogger.Error && (!errors.Is(err, gorm.ErrRecordNotFound) || !l.IgnoreRecordNotFoundError):
		lgr.With("error", err).Errorf("")

	case elapsed > l.SlowThreshold && l.SlowThreshold != 0 && l.LogLevel >= glogger.Warn:
		slowLog := fmt.Sprintf("SLOW SQL >= %v", l.SlowThreshold)
		lgr.With("slowLog", slowLog).Warnf("")

	case l.LogLevel == glogger.Info:
		lgr.Infof("")
	}
}

func getShortFileLine(fileline string) string {
	// 项目根目录，如果目录名称有变动，这里也要同步修改
	arr := strings.Split(fileline, "server_go")
	if len(arr) == 2 {
		return arr[1]
	}
	return fileline
}
