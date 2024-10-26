package logx

import (
	"context"
	"testing"
)

func TestLog(t *testing.T) {
	Debugf("debug msg")

	ctx := context.Background()
	Ctx(ctx).Infof("info msg")

	Ctx(ctx).With("a", 1).With("b", 2).Warnf("warn msg")
	Ctx(ctx).With("a", 1, "b", 2).Warnf("warn msg2")

	ctx = context.WithValue(ctx, ctxKeyReqId, "reqId-123")
	Ctx(ctx).With("c", 3).Errorf("error msg")
}
