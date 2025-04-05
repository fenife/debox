package redisc

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/redis/go-redis/v9"
	"server-go/domain/cache"
	"server-go/domain/do"
	"server-go/domain/entity"
	"strconv"
	"time"
)

const (
	userCacheExpired = 60 * time.Second

	prefixUidToUser  = "uid2user"
	prefixToken2Uid  = "token2uid"
	prefixUid2SignIn = "uid2signin" // 最近一次登陆信息
)

type UserCache struct {
	rds *redis.Client
}

func NewUserCache(rds *redis.Client) *UserCache {
	return &UserCache{
		rds: rds,
	}
}

// UserRepo implements the repo.UserRepo interface
var _ cache.IUserCache = &UserCache{}

func (u *UserCache) CacheUserSignInInfo(ctx context.Context, user *entity.User, signin *do.UserSignInInfo) error {
	userData, err := json.Marshal(user)
	if err != nil {
		return err
	}

	signinData, err := json.Marshal(signin)
	if err != nil {
		return err
	}

	pipe := u.rds.TxPipeline()

	// 保存用户token到id的映射关系, token2uid:<token> -> uid
	pipe.Set(ctx, getKeyToken2Uid(signin.Token), user.ID, userCacheExpired)

	// 保存用户最近一次登陆的信息, uid2signin:<uid> -> signin
	pipe.Set(ctx, getKeyUid2SignIn(user.ID), signinData, userCacheExpired)

	// 根据用户id缓存用户信息, uid2user:<uid> -> user
	pipe.Set(ctx, getKeyUid2User(user.ID), userData, userCacheExpired)

	_, err = pipe.Exec(ctx)
	return err
}

// 根据token获取对应的用户id
func (u *UserCache) getUserIdByToken(ctx context.Context, token string) (uid uint64, err error) {
	uidStr, err := u.rds.Get(ctx, getKeyToken2Uid(token)).Result()
	if err != nil {
		return 0, err
	}
	uid, err = strconv.ParseUint(uidStr, 10, 64)
	return
}

func (u *UserCache) GetUserByToken(ctx context.Context, token string) (*entity.User, error) {
	// 先获取token对应的用户id
	uid, err := u.getUserIdByToken(ctx, token)
	if err != nil {
		return nil, err
	}

	// 根据用户id获取用户信息
	return u.GetUserById(ctx, uid)
}

// 根据用户id获取用户信息
func (u *UserCache) GetUserById(ctx context.Context, userId uint64) (*entity.User, error) {
	userData, err := u.rds.Get(ctx, getKeyUid2User(userId)).Result()
	if err == redis.Nil || userData == "" {
		return &entity.User{}, nil
	}
	if err != nil {
		return nil, err
	}
	var user entity.User
	err = json.Unmarshal([]byte(userData), &user)
	return &user, err
}

func (u *UserCache) DelUserSignInByToken(ctx context.Context, token string) error {
	// 先获取token对应的用户id
	uid, err := u.getUserIdByToken(ctx, token)
	if err != nil {
		return err
	}

	// 删除token到uid的映射关系
	if _, err = u.rds.Del(ctx, getKeyToken2Uid(token)).Result(); err != nil {
		return err
	}

	// 删除用户登陆信息
	_, err = u.rds.Del(ctx, getKeyUid2SignIn(uid)).Result()
	return err
}

// 根据用户id获取最近一次的登陆信息
func (u *UserCache) GetUserSignInInfo(ctx context.Context, userId uint64) (*do.UserSignInInfo, error) {
	signinData, err := u.rds.Get(ctx, getKeyUid2SignIn(userId)).Result()
	if err == redis.Nil || signinData == "" {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	var signin do.UserSignInInfo
	err = json.Unmarshal([]byte(signinData), &signin)
	return &signin, err
}

func getKeyUid2User(uid uint64) string {
	return fmt.Sprintf("%s:%d", prefixUidToUser, uid)
}

func getKeyToken2Uid(token string) string {
	return fmt.Sprintf("%s:%s", prefixToken2Uid, token)
}

func getKeyUid2SignIn(uid uint64) string {
	return fmt.Sprintf("%s:%d", prefixUid2SignIn, uid)
}
