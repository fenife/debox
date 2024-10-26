package repo

import (
	"context"
	"server-go/domain/entity"
)

type IUserRepo interface {
	GetUserList(ctx context.Context) ([]entity.User, error)
}
