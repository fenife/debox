package req

type CreateCategoryReq struct {
	Name string `json:"name" binding:"required,gte=1,lte=20"`
}
