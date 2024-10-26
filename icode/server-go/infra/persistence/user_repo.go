package persistence

import (
	"context"
	"server-go/domain/entity"
	"server-go/domain/repo"

	"gorm.io/gorm"
)

type UserRepo struct {
	db *gorm.DB
}

func NewUserRepo(db *gorm.DB) *UserRepo {
	return &UserRepo{db}
}

// UserRepo implements the repo.UserRepo interface
var _ repo.IUserRepo = &UserRepo{}

func (r *UserRepo) GetUserList(ctx context.Context) ([]entity.User, error) {
	var users []entity.User
	err := r.db.WithContext(ctx).Find(&users).Error
	return users, err
}
