package main

import (
	"github.com/go-gormigrate/gormigrate/v2"
	"gorm.io/gorm"
	"server-go/domain/entity"
)

func init() {
	migrations = append(migrations, &gormigrate.Migration{
		ID: "20240215123000",
		Migrate: func(tx *gorm.DB) error {
			type post struct {
				entity.Post
			}
			// 创建文章表
			return tx.Migrator().CreateTable(&post{})
		},
		Rollback: func(tx *gorm.DB) error {
			return tx.Migrator().DropTable("posts")
		},
	})
}
