package persistence

import (
	"context"
	"errors"
	"server-go/domain/do"
	"server-go/domain/entity"
	"server-go/domain/repo"

	"gorm.io/gorm"
)

type PostRepo struct {
	db *gorm.DB
}

func NewPostRepo(db *gorm.DB) *PostRepo {
	return &PostRepo{db}
}

// UserRepo implements the repo.UserRepo interface
var _ repo.IPostRepo = &PostRepo{}

func (r *PostRepo) GetPostStat(ctx context.Context) ([]do.PostStat, error) {
	var postStats []do.PostStat
	err := r.db.WithContext(ctx).Model(&entity.Post{}).
		Select("cate_id", "count(1) as post_count").Group("cate_id").
		Find(&postStats).Error
	return postStats, err
}

func (r *PostRepo) GetPostList(ctx context.Context, cateId uint64, page, limit int) ([]*entity.Post, error) {
	var posts []*entity.Post
	tx := r.db.WithContext(ctx)
	if cateId > 0 {
		tx = tx.Where("cate_id = ?", cateId)
	}
	offset := (page - 1) * limit
	err := tx.Omit("content").Preload("User").Preload("Category").
		Offset(offset).Limit(limit).Order("id desc").Find(&posts).Error
	return posts, err
}

func (r *PostRepo) GetPostArchiveList(ctx context.Context) ([]*entity.Post, error) {
	// 默认按id倒序排序，亦即创建时间(create_at)
	var posts []*entity.Post
	err := r.db.WithContext(ctx).Preload("User").Preload("Category").
		Omit("content").Order("id desc").Find(&posts).Error
	return posts, err
}

func (r *PostRepo) FindById(ctx context.Context, postId uint64) (*entity.Post, error) {
	var post entity.Post
	err := r.db.WithContext(ctx).Where("id = ?", postId).Preload("User").Preload("Category").First(&post).Error
	if errors.Is(err, gorm.ErrRecordNotFound) {
		// 可通过ID判断是否存在
		return &post, nil
	}
	return &post, err
}

func (r *PostRepo) FindByTitle(ctx context.Context, name string) (*entity.Post, error) {
	var post entity.Post
	err := r.db.WithContext(ctx).Where("title = ?", name).Preload("User").Preload("Category").First(&post).Error
	if errors.Is(err, gorm.ErrRecordNotFound) {
		// 通过ID判断是否存在
		return &post, nil
	}
	return &post, err
}

func (r *PostRepo) SearchByTitle(ctx context.Context, kw string, page, limit int) (posts []*entity.Post, total int, err error) {
	offset := (page - 1) * limit
	err = r.db.WithContext(ctx).Model(&entity.Post{}).Where("title like ?", "%"+kw+"%").Omit("content").
		Preload("User").Preload("Category").Order("id desc").Offset(offset).Limit(limit).Find(&posts).Error
	if err != nil {
		return
	}

	// 总数目
	err = r.db.WithContext(ctx).Model(&entity.Post{}).Where("title like ?", "%"+kw+"%").
		Select("count(1) as total").Scan(&total).Error
	return posts, total, err
}

func (r *PostRepo) GetPrePost(ctx context.Context, postId uint64) (*entity.Post, error) {
	var post entity.Post
	err := r.db.WithContext(ctx).Preload("User").Preload("Category").
		Where("id < ?", postId).Order("id desc").First(&post).Error
	if errors.Is(err, gorm.ErrRecordNotFound) {
		// 可通过ID判断是否存在
		return &post, nil
	}
	return &post, err
}

func (r *PostRepo) GetNextPost(ctx context.Context, postId uint64) (*entity.Post, error) {
	var post entity.Post
	err := r.db.WithContext(ctx).Preload("User").Preload("Category").
		Where("id > ?", postId).Order("id asc").First(&post).Error
	if errors.Is(err, gorm.ErrRecordNotFound) {
		// 可通过ID判断是否存在
		return &post, nil
	}
	return &post, err
}

// 获取可展示的文章总数
func (r *PostRepo) GetPostTotal(ctx context.Context, cateId uint64) (total int, err error) {
	tx := r.db.WithContext(ctx)
	if cateId > 0 {
		tx = tx.Where("cate_id = ?", cateId)
	}
	err = tx.Model(&entity.Post{}).Select("count(1) as total").Scan(&total).Error
	return
}

func (r *PostRepo) CreatePost(ctx context.Context, post *entity.Post) (*entity.Post, error) {
	err := r.db.WithContext(ctx).Create(&post).Error
	return post, err
}
