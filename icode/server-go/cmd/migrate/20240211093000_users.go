package main

import (
	"github.com/go-gormigrate/gormigrate/v2"
	"gorm.io/gorm"
	"server-go/config"
	"server-go/domain/entity"
)

func newAdminUser(adminConf *config.AdminUser) *entity.User {
	admin := entity.User{
		Name: adminConf.Username,
	}
	admin.PasswordHash = admin.GenPasswordHash(adminConf.Password)
	return &admin
}

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

			// 创建管理员
			admin := newAdminUser(&config.Conf.Admin)
			return tx.Create(admin).Error
		},
		Rollback: func(tx *gorm.DB) error {
			return tx.Migrator().DropTable("users")
		},
	})
}
