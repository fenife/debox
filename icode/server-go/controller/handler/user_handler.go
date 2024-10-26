package handler

import (
	"server-go/application/aservice"
	"server-go/controller/req"
	"server-go/internal/errorx"
	"server-go/pkg/logx"
	"server-go/pkg/renderx"

	"github.com/gin-gonic/gin"
)

type UserHandler struct {
	userApp aservice.IUserApp
}

func NewUserHandler(userApp aservice.IUserApp) *UserHandler {
	return &UserHandler{
		userApp: userApp,
	}
}

// GetUserList godoc
// @Summary      用户列表
// @Description  获取用户列表
// @Tags         user
// @Accept       json
// @Produce      json
// @Param        object body  req.GetUserListReq	false "查询参数"
// @Success      200  {object}  renderx.Response
// @Router       /api/v1/user/list [get]
func (ctrl *UserHandler) GetUserList(c *gin.Context) {
	var userReq req.GetUserListReq
	if err := c.ShouldBindJSON(&userReq); err != nil {
		logx.Ctx(c).With("error", err).Errorf("param error")
		renderx.ErrOutput(c, errorx.ParamInvalid)
		return
	}

	users, err := ctrl.userApp.GetUserList(c)
	if err != nil {
		if _, ok := err.(*renderx.Render); !ok {
			logx.Ctx(c).With("error", err).Errorf("get user list failed")
			err = errorx.UserSignupFailed
		}
		renderx.ErrOutput(c, err)
		return
	}
	renderx.SuccOutput(c, users)
}
