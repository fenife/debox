package dservice

import (
	"context"
	"server-go/domain/do"
	"server-go/domain/entity"
	"server-go/domain/repo"
	"server-go/internal/errorx"
)

type IPostDomain interface {
	GetPostStat(ctx context.Context) ([]do.PostStat, error)
	GetPostList(ctx context.Context, cateId uint64, page, limit int) (posts []*entity.Post, total int, err error)
	GetPostById(ctx context.Context, postId uint64) (*entity.Post, error)
	GetPostArchiveList(ctx context.Context) ([]*entity.Post, error)
	GetPostAbout(ctx context.Context) (*entity.Post, error)
	SearchByTitle(ctx context.Context, kw string, page, limit int) (posts []*entity.Post, total int, err error)
	GetPrePost(ctx context.Context, postId uint64) (*entity.Post, error)
	GetNextPost(ctx context.Context, postId uint64) (*entity.Post, error)
	CreatePost(ctx context.Context, post *entity.Post) (*entity.Post, error)
}

type PostDomain struct {
	postRepo repo.IPostRepo
}

func NewPostDomain(postRepo repo.IPostRepo) *PostDomain {
	return &PostDomain{
		postRepo: postRepo,
	}
}

var _ IPostDomain = &PostDomain{}

// 按分类获取文章数目
func (ds *PostDomain) GetPostStat(ctx context.Context) ([]do.PostStat, error) {
	return ds.postRepo.GetPostStat(ctx)
}

// 获取文章列表
func (ds *PostDomain) GetPostList(ctx context.Context, cateId uint64, page, limit int) (posts []*entity.Post, total int, err error) {
	if page <= 0 {
		page = defaultPage // 默认第1页
	}
	if limit <= 0 {
		limit = defaultLimit // 默认一页10条数据
	}
	// 获取文章列表
	posts, err = ds.postRepo.GetPostList(ctx, cateId, page, limit)
	if err != nil {
		return
	}
	total, err = ds.postRepo.GetPostTotal(ctx, cateId)
	return
}

// 获取文章详情
func (ds *PostDomain) GetPostById(ctx context.Context, postId uint64) (*entity.Post, error) {
	post, err := ds.postRepo.FindById(ctx, postId)
	if err != nil {
		return nil, err
	}
	if !post.IsValid() {
		return nil, errorx.PostNotFound
	}
	return post, nil
}

// 获取归档文章列表
func (ds *PostDomain) GetPostArchiveList(ctx context.Context) ([]*entity.Post, error) {
	return ds.postRepo.GetPostArchiveList(ctx)
}

// 获取标题为about的文章，用于about页面内容展示
func (ds *PostDomain) GetPostAbout(ctx context.Context) (*entity.Post, error) {
	post, err := ds.postRepo.FindByTitle(ctx, "about")
	if err != nil {
		return nil, err
	}
	if !post.IsValid() {
		return nil, errorx.PostNotFound
	}
	return post, nil
}

// 根据标题搜索文章
func (ds *PostDomain) SearchByTitle(ctx context.Context, kw string, page, limit int) (posts []*entity.Post, total int, err error) {
	if page <= 0 {
		page = defaultPage // 默认第1页
	}
	if limit <= 0 {
		limit = defaultLimit // 默认一页10条数据
	}
	return ds.postRepo.SearchByTitle(ctx, kw, page, limit)
}

// 获取上一篇文章
func (ds *PostDomain) GetPrePost(ctx context.Context, postId uint64) (*entity.Post, error) {
	post, err := ds.postRepo.GetPrePost(ctx, postId)
	if err != nil {
		return nil, err
	}
	if !post.IsValid() {
		return nil, errorx.PostNotFound
	}
	return post, nil
}

// 获取下一篇文章
func (ds *PostDomain) GetNextPost(ctx context.Context, postId uint64) (*entity.Post, error) {
	post, err := ds.postRepo.GetNextPost(ctx, postId)
	if err != nil {
		return nil, err
	}
	if !post.IsValid() {
		return nil, errorx.PostNotFound
	}
	return post, nil
}

func (ds *PostDomain) CreatePost(ctx context.Context, post *entity.Post) (*entity.Post, error) {
	// 查找文章
	old_post, err := ds.postRepo.FindByTitle(ctx, post.Title)
	if err != nil {
		return nil, err
	}
	// 检查是否已存在
	if old_post.IsValid() {
		return nil, errorx.PostExisted
	}

	return ds.postRepo.CreatePost(ctx, post)
}
