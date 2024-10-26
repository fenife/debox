package gormx

import (
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"server-go/config"
)

func NewGormMysqlDB(mysqlConf *config.MysqlConfig) (*gorm.DB, error) {
	db, err := gorm.Open(mysql.Open(mysqlConf.ConnStr()), &gorm.Config{
		//	Logger: logger.Default.LogMode(logger.Info),
		Logger: NewGormLogger(),
	})

	return db, err
}
