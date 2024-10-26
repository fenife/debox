package dservice

import (
	"server-go/domain/repo"
)

const (
	defaultPage  = 1
	defaultLimit = 10
)

type DomainServices struct {
	UserDomain IUserDomain
}

func NewDomainServices(userRepo repo.IUserRepo) *DomainServices {
	return &DomainServices{
		UserDomain: NewUserDomain(userRepo),
	}
}
