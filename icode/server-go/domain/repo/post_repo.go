package repo

import (
	"context"
	"server-go/domain/do"
	"server-go/domain/entity"
)

type IPostRepo interface {
	GetPostStat(ctx context.Context) ([]do.PostStat, error)
	GetPostList(ctx context.Context, cateId uint64, page, limit int) ([]*entity.Post, error)
	FindById(ctx context.Context, postId uint64) (*entity.Post, error)
	GetPostArchiveList(ctx context.Context) ([]*entity.Post, error)
	FindByTitle(ctx context.Context, name string) (*entity.Post, error)
	SearchByTitle(ctx context.Context, kw string, page, limit int) (posts []*entity.Post, total int, err error)
	GetPrePost(ctx context.Context, postId uint64) (*entity.Post, error)
	GetNextPost(ctx context.Context, postId uint64) (*entity.Post, error)
	GetPostTotal(ctx context.Context, cateId uint64) (total int, err error)
	CreatePost(ctx context.Context, post *entity.Post) (*entity.Post, error)
}
