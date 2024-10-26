package aservice

import (
	"server-go/domain/dservice"
)

const timeFormatLayout = "2006-01-02 15:05:05"

type Apps struct {
	UserApp IUserApp
}

func NewApps(userDomain dservice.IUserDomain) *Apps {
	return &Apps{
		UserApp: NewUserApp(userDomain),
	}
}
