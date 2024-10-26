package middleware

import (
	"bytes"
	"encoding/json"
	"github.com/gin-gonic/gin"
	"io"
	"server-go/pkg/logx"
	"strings"
	"time"
)

type bodyLogWriter struct {
	gin.ResponseWriter
	body *bytes.Buffer
}

func (w bodyLogWriter) Write(b []byte) (int, error) {
	w.body.Write(b)
	return w.ResponseWriter.Write(b)
}

func LogContext() gin.HandlerFunc {
	return func(c *gin.Context) {
		t := time.Now()
		// 获取请求body数据
		bodyData, _ := io.ReadAll(c.Request.Body)
		c.Request.Body = io.NopCloser(bytes.NewReader(bodyData))

		// 双写
		writer := &bodyLogWriter{body: bytes.NewBufferString(""), ResponseWriter: c.Writer}
		c.Writer = writer

		// 请求处理
		c.Next()

		// log记录请求和响应信息
		path := c.Request.URL.Path
		withArgs := []interface{}{
			"method", c.Request.Method,
			"url", c.Request.RequestURI,
			"path", path,
			"body", string(bodyData),
			"internal", time.Since(t).Milliseconds(), // 毫秒
			"status", c.Writer.Status(),
		}

		if needToLogResponse(path) {
			// 再解析一次，方便日志查看，会有性能损耗
			var respData interface{}
			if err := json.Unmarshal(writer.body.Bytes(), &respData); err != nil {
				logx.Ctx(c).With("error", err).Errorf("unmarshal response failed")
				respData = writer.body.String()
			}

			// 记录响应body及其长度
			withArgs = append(withArgs, "response", respData, "resp_len", writer.body.Len())
		}
		logx.Ctx(c).With(withArgs...).Infof("")
	}
}

// 判断是否需要记录响应体
func needToLogResponse(path string) bool {
	// swag文档api接口，不需要 log response body
	if strings.Contains(path, "swagger") {
		return false
	}
	return true
}
