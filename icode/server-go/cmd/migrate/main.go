package main

import (
	"github.com/go-gormigrate/gormigrate/v2"
	"server-go/config"
	"server-go/pkg/gormx"
	"server-go/pkg/logx"
)

var migrations = make([]*gormigrate.Migration, 0)

func main() {
	db, err := gormx.NewGormMysqlDB(&config.Conf.Mysql)
	if err != nil {
		logx.Fatalf("init db failed: %v", err)
	}

	m := gormigrate.New(db, gormigrate.DefaultOptions, migrations)
	if err = m.Migrate(); err != nil {
		logx.Fatalf("migration failed: %v", err)
	}
	logx.Infof("migration run finish")
}
