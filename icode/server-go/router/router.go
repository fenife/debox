package router

import (
	"server-go/application/aservice"
	"server-go/config"
	"server-go/controller/handler"
	"server-go/domain/dservice"
	"server-go/infra/cache/redisc"
	"server-go/infra/persistence"

	"github.com/gin-gonic/gin"
	// swaggerFiles "github.com/swaggo/files"
	// ginSwagger "github.com/swaggo/gin-swagger"
)

func AddRouter(engine *gin.Engine) {
	// swag文档
	// engine.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	// 资源初始化
	repos, err := persistence.NewRepos(&config.Conf.Mysql)
	if err != nil {
		panic(err)
	}
	_, err = redisc.NewCaches(&config.Conf.Redis)
	if err != nil {
		panic(err)
	}
	domainServices := dservice.NewDomainServices(repos.UserRepo)
	apps := aservice.NewApps(domainServices.UserDomain)
	hdr := handler.NewHandlers(apps.UserApp)

	// 匹配所有路由
	engine.GET("/*any", hdr.PingHandler.Ping)

	// 添加路由
	// engine.GET("/ping", hdr.PingHandler.Ping)

	// apiV1 := engine.Group("/api/v1")
	// {
	// 	user := apiV1.Group("user")
	// 	{
	// 		user.GET("/list", hdr.UserHandler.GetUserList)
	// 	}
	// }
}
