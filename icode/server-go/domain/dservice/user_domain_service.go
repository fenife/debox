package dservice

import (
	"context"
	"server-go/domain/cache"
	"server-go/domain/do"
	"server-go/domain/entity"
	"server-go/domain/repo"
	"server-go/internal/errorx"
	"server-go/pkg/logx"
	"time"
)

type IUserDomain interface {
	Signup(ctx context.Context, user *entity.User) (*entity.User, error)
	SignIn(ctx context.Context, name, password string) (user *entity.User, signin *do.UserSignInInfo, err error)
	SignOut(ctx context.Context, token string) (err error)
	GetUserByName(ctx context.Context, name string) (*entity.User, error)
	GetUserById(ctx context.Context, userId uint64) (*entity.User, error)
	UserExisted(ctx context.Context, name string) (bool, error)
	GetUserList(ctx context.Context) ([]entity.User, error)
	FindByToken(ctx context.Context, userToken string) (*entity.User, error)
}

type UserDomain struct {
	userRepo  repo.IUserRepo
	userCache cache.IUserCache
}

func NewUserDomain(userRepo repo.IUserRepo, userCache cache.IUserCache) *UserDomain {
	return &UserDomain{
		userRepo:  userRepo,
		userCache: userCache,
	}
}

var _ IUserDomain = &UserDomain{}

// 用户注册
func (ds *UserDomain) Signup(ctx context.Context, user *entity.User) (*entity.User, error) {
	// 用户已经存在
	existed, err := ds.UserExisted(ctx, user.Name)
	if err != nil {
		return nil, err
	}
	if existed {
		return nil, errorx.UserExisted
	}

	return ds.userRepo.CreateUser(ctx, user)
}

func (ds *UserDomain) UserExisted(ctx context.Context, name string) (bool, error) {
	user, err := ds.userRepo.FindByName(ctx, name)
	if err != nil {
		return false, err
	}
	if user.ID <= 0 {
		return false, nil
	}
	return true, nil
}

func (ds *UserDomain) GetUserByName(ctx context.Context, name string) (*entity.User, error) {
	return ds.userRepo.FindByName(ctx, name)
}

func (ds *UserDomain) GetUserById(ctx context.Context, userId uint64) (*entity.User, error) {
	user, err := ds.userRepo.FindById(ctx, userId)
	if err != nil {
		return nil, err
	}
	if !user.IsValid() {
		return nil, errorx.UserNotFound
	}
	return user, nil
}

func (ds *UserDomain) GetUserList(ctx context.Context) ([]entity.User, error) {
	return ds.userRepo.GetUserList(ctx)
}

func (ds *UserDomain) FindByToken(ctx context.Context, userToken string) (*entity.User, error) {
	return nil, nil
}

// 用户登陆
func (ds *UserDomain) SignIn(ctx context.Context, name, password string) (user *entity.User, signin *do.UserSignInInfo, err error) {
	// 查找用户
	user, err = ds.userRepo.FindByName(ctx, name)
	if err != nil {
		return
	}
	// 检查用户是否存在
	if !user.IsValid() {
		return nil, nil, errorx.UserNotExisted
	}
	// 检查密码是否错误
	pwHash := user.GenPasswordHash(password)
	if user.PasswordHash != pwHash {
		logx.Ctx(ctx).Errorf("password is not valid: %s != %s", user.PasswordHash, pwHash)
		return nil, nil, errorx.UserNameOrPasswdNotValid
	}

	// 检查是否已经登陆，限制一段时间内的登陆次数，防止接口频繁被调用而生成很多缓存数据
	signin, err = ds.userCache.GetUserSignInInfo(ctx, user.ID)
	if err != nil {
		return nil, nil, err
	}
	if signin != nil && signin.IsSignInLimit() {
		return nil, nil, errorx.UserAlreadySignIn
	}

	// 生成用户登陆信息
	signin = &do.UserSignInInfo{
		UserId: user.ID,
		Token:  user.GenUserToken(),
		SignTs: time.Now().Unix(),
	}

	// 缓存用户登陆信息
	if err = ds.userCache.CacheUserSignInInfo(ctx, user, signin); err != nil {
		return nil, nil, err
	}
	return
}

// 用户退出
func (ds *UserDomain) SignOut(ctx context.Context, token string) (err error) {
	// 删除缓存信息
	return ds.userCache.DelUserSignInByToken(ctx, token)
}
