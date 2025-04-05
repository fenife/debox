package repo

import (
	"context"
	"server-go/domain/entity"
)

type ICategoryRepo interface {
	GetCategoryList(ctx context.Context) ([]entity.Category, error)
	FindById(ctx context.Context, cateId uint64) (*entity.Category, error)
	CreateCategory(ctx context.Context, cate *entity.Category) (*entity.Category, error)
	FindByName(ctx context.Context, name string) (*entity.Category, error)
}
