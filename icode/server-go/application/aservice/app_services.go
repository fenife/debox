package aservice

import (
	"server-go/domain/dservice"
)

const timeFormatLayout = "2006-01-02 15:05:05"

type Apps struct {
	UserApp     IUserApp
	CategoryApp ICategoryApp
	PostApp     IPostApp
}

func NewApps(userDomain dservice.IUserDomain, categoryDomain dservice.ICategoryDomain, postDomain dservice.IPostDomain) *Apps {
	return &Apps{
		UserApp:     NewUserApp(userDomain),
		CategoryApp: NewCategoryApp(categoryDomain, postDomain),
		PostApp:     NewPostApp(postDomain, categoryDomain, userDomain),
	}
}
