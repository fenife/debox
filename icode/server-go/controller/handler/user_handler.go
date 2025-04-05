package handler

import (
	"github.com/gin-gonic/gin"
	"server-go/application/aservice"
	"server-go/controller/req"
	"server-go/controller/resp"
	"server-go/internal/errorx"
	"server-go/internal/gctx"
	"server-go/pkg/logx"
	"server-go/pkg/renderx"
)

type UserHandler struct {
	userApp aservice.IUserApp
}

func NewUserHandler(userApp aservice.IUserApp) *UserHandler {
	return &UserHandler{
		userApp: userApp,
	}
}

// UserSignup godoc
// @Summary      用户注册
// @Description  创建新用户
// @Tags         user
// @Accept       json
// @Produce      json
// @Param        object body  req.SignupReq	false "查询参数"
// @Success      200  {object}  renderx.Response
// @Router       /api/v1/user/signup [post]
func (ctrl *UserHandler) UserSignup(c *gin.Context) {
	var userReq req.SignupReq
	if err := c.ShouldBindJSON(&userReq); err != nil {
		logx.Ctx(c).With("error", err).Errorf("param error")
		renderx.ErrOutput(c, errorx.ParamInvalid)
		return
	}

	_, err := ctrl.userApp.Signup(c, userReq.Name, userReq.Password)
	if err != nil {
		if _, ok := err.(*renderx.Render); !ok {
			logx.Ctx(c).With("error", err).Errorf("create user failed")
			err = errorx.UserSignupFailed
		}
		renderx.ErrOutput(c, err)
		return
	}
	renderx.SuccOutput(c)
}

// UserSignIn godoc
// @Summary      用户登陆
// @Description	 检查用户是否存在，密码是否正确，如果正常，返回用户token
// @Tags         user
// @Accept       json
// @Produce      json
// @Param        object body  req.SignInReq	false "查询参数"
// @Success      200  {object}  resp.SignInResp
// @Failure      111001  integer 	"参数错误"
// @Router       /api/v1/user/signin [post]
func (ctrl *UserHandler) UserSignIn(c *gin.Context) {
	var userReq req.SignInReq
	if err := c.ShouldBindJSON(&userReq); err != nil {
		logx.Ctx(c).With("error", err).Errorf("param error")
		renderx.ErrOutput(c, errorx.ParamInvalid)
		return
	}

	user, signin, err := ctrl.userApp.SignIn(c, userReq.Name, userReq.Password)
	if err != nil {
		if _, ok := err.(*renderx.Render); !ok {
			logx.Ctx(c).With("error", err).Errorf("user sign in failed")
			err = errorx.UserSignupFailed
		}
		renderx.ErrOutput(c, err)
		return
	}

	data := resp.SignInResp{
		UserName:  user.Name,
		UserToken: signin.Token,
	}
	renderx.SuccOutput(c, data)
}

// UserSignOut godoc
// @Summary      用户退出
// @Description	 用户退出登陆，需要在header中附带x-user-token参数
// @Tags         user
// @Accept       json
// @Produce      json
// @Success      200  {object}  renderx.Response
// @Router       /api/v1/user/signout [post]
func (ctrl *UserHandler) UserSignOut(c *gin.Context) {
	token := gctx.GetUserToken(c)
	err := ctrl.userApp.SignOut(c, token)
	if err != nil {
		if _, ok := err.(*renderx.Render); !ok {
			logx.Ctx(c).With("error", err).Errorf("user sign out failed")
			err = errorx.UserSignOutFailed
		}
		renderx.ErrOutput(c, err)
		return
	}
	renderx.SuccOutput(c)
}
