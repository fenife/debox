package router

import (
	"server-go/application/aservice"
	"server-go/config"
	"server-go/controller/handler"
	mw "server-go/controller/middleware"
	"server-go/domain/dservice"
	"server-go/infra/cache/redisc"
	"server-go/infra/persistence"

	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

func AddRouter(engine *gin.Engine) {
	// swag文档
	engine.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	// 资源初始化
	repos, err := persistence.NewRepos(&config.Conf.Mysql)
	if err != nil {
		panic(err)
	}
	caches, err := redisc.NewCaches(&config.Conf.Redis)
	if err != nil {
		panic(err)
	}
	domainServices := dservice.NewDomainServices(repos.UserRepo, caches.UserCache, repos.CategoryRepo, repos.PostRepo)
	apps := aservice.NewApps(domainServices.UserDomain, domainServices.CategoryDomain, domainServices.PostDomain)
	hdr := handler.NewHandlers(apps.UserApp, apps.CategoryApp, apps.PostApp)

	// 添加路由
	engine.GET("/ping", hdr.PingHandler.Ping)
	apiV1 := engine.Group("/api/v1")
	{
		user := apiV1.Group("user")
		{
			user.POST("/signup", hdr.UserHandler.UserSignup)
			user.POST("/signin", hdr.UserHandler.UserSignIn)
			user.POST("/signout", mw.UserAuthMiddleware(caches.UserCache), hdr.UserHandler.UserSignOut)
		}
		cate := apiV1.Group("category")
		{
			cate.GET("/list", hdr.CategoryHandler.GetCategoryList)
			cate.POST("", hdr.CategoryHandler.CreateCategory)
		}

		post := apiV1.Group("post")
		{
			post.GET("/list", hdr.PostHandler.GetPostList)
			post.GET("/detail", mw.ApiCacheMiddleware(caches.ApiCache), hdr.PostHandler.GetPostDetail)
			post.GET("/archive", hdr.PostHandler.GetPostArchive)
			post.GET("/about", mw.ApiCacheMiddleware(caches.ApiCache), hdr.PostHandler.GetPostAbout)
			post.GET("/search", mw.ApiCacheMiddleware(caches.ApiCache), hdr.PostHandler.SearchPostByTitle)
			post.POST("", hdr.PostHandler.CreatePost)
		}
	}
}
