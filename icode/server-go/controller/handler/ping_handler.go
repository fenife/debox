package handler

import (
	"github.com/gin-gonic/gin"
	"server-go/pkg/renderx"
)

type PingHandler struct{}

func NewPingHandler() *PingHandler {
	return &PingHandler{}
}

// Ping godoc
// @Summary      ping,检查服务是否正常
// @Tags         ping
// @Produce      json
// @Success      200  {object}  renderx.Response
// @Router       /ping [get]
func (ctrl *PingHandler) Ping(c *gin.Context) {
	renderx.SuccOutput(c)
}
