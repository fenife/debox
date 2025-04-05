package handler

import (
	"server-go/application/aservice"
	"server-go/controller/req"
	"server-go/controller/resp"
	"server-go/internal/errorx"
	"server-go/pkg/logx"
	"server-go/pkg/renderx"

	"github.com/gin-gonic/gin"
)

type CategoryHandler struct {
	cateApp aservice.ICategoryApp
}

func NewCategoryHandler(cateApp aservice.ICategoryApp) *CategoryHandler {
	return &CategoryHandler{
		cateApp: cateApp,
	}
}

// GetCategoryList godoc
// @Summary      分类列表
// @Description	 获取文章分类列表，包含了该分类下文章的统计数目
// @Tags         category
// @Accept       json
// @Produce      json
// @Success      200  {object}  resp.CategoryListResp
// @Router       /api/v1/category/list [get]
func (ctrl *CategoryHandler) GetCategoryList(c *gin.Context) {
	// 暂时不分页返回全部分类
	cateList, err := ctrl.cateApp.GetCategoryList(c)
	if err != nil {
		if _, ok := err.(*renderx.Render); !ok {
			logx.Ctx(c).With("error", err).Errorf("get category list failed")
			err = errorx.CateListFailed
		}
		renderx.ErrOutput(c, err)
		return
	}

	result := resp.CategoryListResp{
		Total:    len(cateList),
		CateList: cateList,
	}

	renderx.SuccOutput(c, result)
}

// CreateCategory godoc
// @Summary      新增分类
// @Description	 新增分类
// @Tags         category
// @Accept       json
// @Produce      json
// @Param        object body  req.CreateCategoryReq	false "参数"
// @Success      200  {object}  renderx.Response
// @Router       /api/v1/category [post]
func (ctrl *CategoryHandler) CreateCategory(c *gin.Context) {
	var cateReq req.CreateCategoryReq
	if err := c.ShouldBindJSON(&cateReq); err != nil {
		logx.Ctx(c).With("error", err).Errorf("param error")
		renderx.ErrOutput(c, errorx.ParamInvalid)
		return
	}

	_, err := ctrl.cateApp.CreateCategory(c, cateReq.Name)
	if err != nil {
		if _, ok := err.(*renderx.Render); !ok {
			logx.Ctx(c).With("error", err).Errorf("create category failed")
			err = errorx.CreateCategoryFailed
		}
		renderx.ErrOutput(c, err)
		return
	}
	renderx.SuccOutput(c)
}
