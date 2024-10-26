package do

type UserTiny struct {
	ID   uint64 `json:"id"`
	Name string `json:"name"`
}

type UserSmall struct {
	ID        uint64 `json:"id"`
	CreatedAt string `json:"created_at"` // "2006-01-02 15:05:05"
	UpdatedAt string `json:"updated_at"` // 同上
	Name      string `json:"name"`
}
