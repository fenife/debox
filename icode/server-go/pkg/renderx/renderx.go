package renderx

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"server-go/internal/gctx"
)

type Result struct {
	Code int    `json:"code"`
	Msg  string `json:"msg"`
}

type Response struct {
	Result Result      `json:"result"`
	Data   interface{} `json:"data"`
}

type Render struct {
	StatusCode int
	Response   Response
}

func (r *Render) Error() string {
	return r.Response.Result.Msg
}

func NewRender(statusCode, code int, msg string, data ...interface{}) *Render {
	r := &Render{
		StatusCode: statusCode,
		Response: Response{
			Result: Result{
				Code: code,
				Msg:  msg,
			},
			Data: nil,
		},
	}
	if len(data) > 0 {
		r.Response.Data = data[0]
	}
	return r
}

const (
	ErrCodeOK     = 0
	ErrCodeFailed = 1
)

var (
	RespOK     = NewRender(http.StatusOK, ErrCodeOK, "ok")
	RespFailed = NewRender(http.StatusInternalServerError, ErrCodeFailed, "failed")
)

// 响应头中返回 request id
func setRespHeaderReqId(c *gin.Context) {
	reqId := gctx.GetReqId(c)
	if reqId != "" {
		c.Writer.Header().Set(gctx.HeaderKeyReqId, reqId)
	}
}

func ErrOutput(c *gin.Context, err interface{}) {
	setRespHeaderReqId(c)

	r, ok := err.(*Render)
	if ok {
		c.JSON(r.StatusCode, r.Response)
		return
	}

	e, ok := err.(error)
	if ok {
		r = NewRender(http.StatusInternalServerError, ErrCodeFailed, e.Error())
		c.JSON(r.StatusCode, r.Response)
		return
	}

	c.JSON(RespFailed.StatusCode, RespFailed.Response)
	return
}

func SuccOutput(c *gin.Context, data ...interface{}) {
	setRespHeaderReqId(c)

	if len(data) == 0 {
		c.JSON(RespOK.StatusCode, RespOK.Response)
		return
	}

	d := data[0]
	r, ok := d.(*Render)
	if ok {
		c.JSON(r.StatusCode, r.Response)
		return
	}
	res, ok := d.(*Response)
	if ok {
		c.JSON(RespOK.StatusCode, res)
		return
	}

	// 用data生成新的resp
	r = NewRender(http.StatusOK, ErrCodeOK, "ok", d)
	c.JSON(r.StatusCode, r.Response)
	return
}
