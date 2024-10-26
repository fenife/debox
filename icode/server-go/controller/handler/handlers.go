package handler

import (
	"server-go/application/aservice"
)

type Handlers struct {
	PingHandler *PingHandler
	UserHandler *UserHandler
}

func NewHandlers(userApp aservice.IUserApp) *Handlers {
	return &Handlers{
		PingHandler: NewPingHandler(),
		UserHandler: NewUserHandler(userApp),
	}
}
