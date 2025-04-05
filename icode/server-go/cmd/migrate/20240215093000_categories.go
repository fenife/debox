package main

import (
	"github.com/go-gormigrate/gormigrate/v2"
	"gorm.io/gorm"
	"server-go/domain/entity"
)

func init() {
	migrations = append(migrations, &gormigrate.Migration{
		ID: "20240215093000",
		Migrate: func(tx *gorm.DB) error {
			type category struct {
				entity.Category
			}
			// 创建分类表
			return tx.Migrator().CreateTable(&category{})
		},
		Rollback: func(tx *gorm.DB) error {
			return tx.Migrator().DropTable("categories")
		},
	})
}
