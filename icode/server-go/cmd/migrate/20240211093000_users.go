package main

import (
	"server-go/domain/entity"

	"github.com/go-gormigrate/gormigrate/v2"
	"gorm.io/gorm"
)

func init() {
	migrations = append(migrations, &gormigrate.Migration{
		ID: "20240211093000",
		Migrate: func(tx *gorm.DB) error {
			type user struct {
				entity.User
			}

			// 创建用户表
			if err := tx.Migrator().CreateTable(&user{}); err != nil {
				return err
			}

			return nil
		},
		Rollback: func(tx *gorm.DB) error {
			return tx.Migrator().DropTable("users")
		},
	})
}
