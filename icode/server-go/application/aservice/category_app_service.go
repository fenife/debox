package aservice

import (
	"context"
	"server-go/application/dto"
	"server-go/domain/do"
	"server-go/domain/dservice"
	"server-go/domain/entity"
	"sort"
	"strings"
)

type ICategoryApp interface {
	GetCategoryList(ctx context.Context) ([]dto.CategoryListItem, error)
	CreateCategory(ctx context.Context, name string) (*entity.Category, error)
}

type CategoryApp struct {
	categoryDomain dservice.ICategoryDomain
	postDomain     dservice.IPostDomain
}

func NewCategoryApp(categoryDomain dservice.ICategoryDomain, postDomain dservice.IPostDomain) *CategoryApp {
	return &CategoryApp{
		categoryDomain: categoryDomain,
		postDomain:     postDomain,
	}
}

var _ ICategoryApp = &CategoryApp{}

func (app *CategoryApp) GetCategoryList(ctx context.Context) ([]dto.CategoryListItem, error) {
	cates, err := app.categoryDomain.GetCategoryList(ctx)
	if err != nil {
		return nil, err
	}
	postStat, err := app.postDomain.GetPostStat(ctx)
	if err != nil {
		return nil, err
	}

	// list -> map
	statMaps := make(map[uint64]do.PostStat, 0)
	for _, p := range postStat {
		statMaps[p.CateId] = p
	}

	res := make([]dto.CategoryListItem, 0)
	for _, c := range cates {
		d := dto.CategoryListItem{
			CategoryTiny: c.ToTiny(),
		}
		// 该分类下可展示文章的数目
		if p, ok := statMaps[c.ID]; ok {
			d.PostCount = p.PostCount
		}
		res = append(res, d)
	}

	// 排序，按文章数目倒序，按名称正序
	sort.SliceStable(res, func(i, j int) bool {
		if res[i].PostCount != res[j].PostCount {
			return res[i].PostCount > res[j].PostCount
		}
		return strings.Compare(res[i].Name, res[j].Name) == -1
	})

	return res, nil
}

// 新增分类
func (app *CategoryApp) CreateCategory(ctx context.Context, name string) (*entity.Category, error) {
	cate := entity.Category{
		Name: name,
	}
	return app.categoryDomain.CreateCategory(ctx, &cate)
}
