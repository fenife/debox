package aservice

import (
	"context"
	"server-go/application/dto"
	"server-go/controller/req"
	"server-go/domain/do"
	"server-go/domain/dservice"
	"server-go/domain/entity"
	"server-go/pkg/logx"
	"server-go/pkg/md2html"
	"sort"
)

const (
	contentTypeMd   = "md"
	contentTypeHtml = "html"
)

type IPostApp interface {
	GetPostList(ctx context.Context, cateId uint64, page, limit int) (posts []*do.PostDetail, total int, err error)
	GetPostDetail(ctx context.Context, postId uint64, contentType string) (*dto.PostDetailWithPreNext, error)
	GetPostArchiveList(ctx context.Context) ([]*dto.PostArchiveItem, error)
	GetPostAbout(ctx context.Context, contentType string) (*dto.PostDetailWithPreNext, error)
	SearchPostByTitle(ctx context.Context, kw string, page, limit int) (posts []*do.PostDetail, total int, err error)
	CreatePost(ctx context.Context, req *req.CreatePostReq) (*entity.Post, error)
}

type PostApp struct {
	postDomain dservice.IPostDomain
	cateDomain dservice.ICategoryDomain
	userDomain dservice.IUserDomain
}

func NewPostApp(postDomain dservice.IPostDomain, cateDomain dservice.ICategoryDomain,
	userDomain dservice.IUserDomain) *PostApp {
	return &PostApp{
		postDomain: postDomain,
		cateDomain: cateDomain,
		userDomain: userDomain,
	}
}

var _ IPostApp = &PostApp{}

// 获取文章列表
func (app *PostApp) GetPostList(ctx context.Context, cateId uint64, page, limit int) (postList []*do.PostDetail, total int, err error) {
	posts, total, err := app.postDomain.GetPostList(ctx, cateId, page, limit)
	if err != nil {
		return
	}
	postList = make([]*do.PostDetail, 0)
	for _, p := range posts {
		postList = append(postList, p.ToDetail())
	}
	return postList, total, err
}

// 获取文章详情
func (app *PostApp) GetPostDetail(ctx context.Context, postId uint64, contentType string) (*dto.PostDetailWithPreNext, error) {
	post, err := app.postDomain.GetPostById(ctx, postId)
	if err != nil {
		return nil, err
	}
	detail, err := app.postToDetailWithContent(post, contentType)
	if err != nil {
		return nil, err
	}
	prePost, err := app.postDomain.GetPrePost(ctx, post.ID)
	if err != nil {
		logx.Ctx(ctx).With("error", err).Errorf("get pre post failed: %v", err)
	}
	nextPost, err := app.postDomain.GetNextPost(ctx, post.ID)
	if err != nil {
		logx.Ctx(ctx).With("error", err).Errorf("get next post failed: %v", err)
	}
	result := dto.PostDetailWithPreNext{
		Post: detail,
		Pre:  prePost.ToDetail(),
		Next: nextPost.ToDetail(),
	}
	return &result, nil
}

func (app *PostApp) GetPostAbout(ctx context.Context, contentType string) (*dto.PostDetailWithPreNext, error) {
	post, err := app.postDomain.GetPostAbout(ctx)
	if err != nil {
		return nil, err
	}
	detail, err := app.postToDetailWithContent(post, contentType)
	if err != nil {
		return nil, err
	}
	result := dto.PostDetailWithPreNext{
		Post: detail,
		Pre:  nil,
		Next: nil,
	}
	return &result, nil
}

// 获取归档文章列表
func (app *PostApp) GetPostArchiveList(ctx context.Context) ([]*dto.PostArchiveItem, error) {
	posts, err := app.postDomain.GetPostArchiveList(ctx)
	if err != nil {
		return nil, err
	}
	// 按年份将文章分类
	// 默认按id倒序排序，亦即创建时间(create_at)
	yearMap := make(map[int]*dto.PostArchiveItem, 0)
	for _, v := range posts {
		p := v
		year := p.CreatedAt.Year()
		if _, ok := yearMap[year]; !ok {
			yearMap[year] = &dto.PostArchiveItem{
				Year:     year,
				Count:    0,
				PostList: make([]*do.PostDetail, 0),
			}
		}
		detail := p.ToDetail()

		yearMap[year].PostList = append(yearMap[year].PostList, detail)
		yearMap[year].Count += 1
	}

	result := make([]*dto.PostArchiveItem, 0)
	for _, v := range yearMap {
		p := v
		result = append(result, p)
	}
	// 按年份倒序排序
	sort.SliceStable(result, func(i, j int) bool {
		return result[i].Year > result[j].Year
	})
	return result, err
}

// domain对象转换
func (app *PostApp) postToDetailWithContent(post *entity.Post, contentType string) (*dto.PostDetail, error) {
	if contentType == "" {
		contentType = contentTypeHtml
	}
	detail := &dto.PostDetail{
		PostDetail: post.ToDetail(),
	}
	switch contentType {
	case contentTypeMd:
		detail.Content = post.Content
	case contentTypeHtml:
		detail.Content = md2html.Parse(post.Content)
	}
	return detail, nil
}

func (app *PostApp) SearchPostByTitle(ctx context.Context, kw string, page, limit int) (posts []*do.PostDetail, total int, err error) {
	postList, total, err := app.postDomain.SearchByTitle(ctx, kw, page, limit)
	if err != nil {
		return
	}
	posts = make([]*do.PostDetail, 0)
	for _, v := range postList {
		p := v
		posts = append(posts, p.ToDetail())
	}
	return
}

func (app *PostApp) CreatePost(ctx context.Context, req *req.CreatePostReq) (*entity.Post, error) {
	post := entity.Post{
		UserId:  req.UserId,
		CateId:  req.CateId,
		Title:   req.Title,
		TitleEn: req.TitleEn,
		Content: req.Content,
	}
	return app.postDomain.CreatePost(ctx, &post)
}
