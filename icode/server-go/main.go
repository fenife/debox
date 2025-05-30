package main

import (
	"fmt"
	"server-go/config"
	mw "server-go/controller/middleware"
	"server-go/router"

	"github.com/gin-gonic/gin"

	_ "server-go/docs" // 导入swag生成的接口文档
)

// @title yonder blog api aservice
// @version 1.0
// @description 后端API服务
// @termsOfService https://github.com/swaggo/swag
// @host localhost:8020
// @BasePath /
func main() {
	engine := gin.New()
	//gin.SetMode(gin.ReleaseMode)

	engine.Use(
		mw.RequestIdMiddleware(),
		mw.LogContext(),
		gin.Recovery(),
	)

	router.AddRouter(engine)

	if err := engine.Run(config.Conf.Server.ServerAddr()); err != nil {
		panic(fmt.Sprintf("start app failed: %v", err))
	}
}
