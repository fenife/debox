package main

import (
	"fmt"
	"os"

	"github.com/gin-gonic/gin"
)

const ADDR = "0.0.0.0:6000"

func ping(c *gin.Context) {
	hostname, _ := os.Hostname()
	c.JSON(200, gin.H{
		"message": fmt.Sprintf("pong %s", hostname),
	})
}

func main() {
	r := gin.Default()
	r.GET("/", ping)
	r.GET("/ping", ping)
	r.Run(ADDR)
}
