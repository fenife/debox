package persistence

import (
	"context"
	"errors"
	"gorm.io/gorm"
	"server-go/domain/entity"
	"server-go/domain/repo"
)

type UserRepo struct {
	db *gorm.DB
}

func NewUserRepo(db *gorm.DB) *UserRepo {
	return &UserRepo{db}
}

// UserRepo implements the repo.UserRepo interface
var _ repo.IUserRepo = &UserRepo{}

func (r *UserRepo) CreateUser(ctx context.Context, user *entity.User) (*entity.User, error) {
	err := r.db.WithContext(ctx).Create(&user).Error
	return user, err
}

func (r *UserRepo) FindByName(ctx context.Context, name string) (*entity.User, error) {
	var user entity.User
	err := r.db.WithContext(ctx).Where("name = ?", name).First(&user).Error
	if errors.Is(err, gorm.ErrRecordNotFound) {
		// 通过user.ID判断是否存在
		return &user, nil
	}
	return &user, err
}

func (r *UserRepo) FindById(ctx context.Context, userId uint64) (*entity.User, error) {
	var user entity.User
	err := r.db.WithContext(ctx).Where("id = ?", userId).First(&user).Error
	if errors.Is(err, gorm.ErrRecordNotFound) {
		// 通过user.ID判断是否存在
		return &user, nil
	}
	return &user, err
}

func (r *UserRepo) GetUserList(ctx context.Context) ([]entity.User, error) {
	var users []entity.User
	err := r.db.WithContext(ctx).Find(&users).Error
	return users, err
}
