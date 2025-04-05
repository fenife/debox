package handler

import (
	"server-go/application/aservice"
)

type Handlers struct {
	PingHandler     *PingHandler
	UserHandler     *UserHandler
	CategoryHandler *CategoryHandler
	PostHandler     *PostHandler
}

func NewHandlers(userApp aservice.IUserApp, cateApp aservice.ICategoryApp, postApp aservice.IPostApp) *Handlers {
	return &Handlers{
		PingHandler:     NewPingHandler(),
		UserHandler:     NewUserHandler(userApp),
		CategoryHandler: NewCategoryHandler(cateApp),
		PostHandler:     NewPostHandler(postApp),
	}
}
