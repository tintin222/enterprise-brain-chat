// Copyright (c) 2015-present Mattermost, Inc. All Rights Reserved.
// See LICENSE.txt for license information.

package api4

import (
	"context"
	"net/http"
	"testing"

	"github.com/stretchr/testify/require"
)

// Enterprise Brain: the upgrade to Mattermost Enterprise Edition, which would replace this build, is not offered.
func TestUpgradeToEnterpriseNotOffered(t *testing.T) {
	th := Setup(t).InitBasic(t)

	resp, err := th.SystemAdminClient.DoAPIPost(context.Background(), "/upgrade_to_enterprise", "")
	require.Error(t, err)
	require.Equal(t, http.StatusNotImplemented, resp.StatusCode)

	resp, err = th.SystemAdminClient.DoAPIGet(context.Background(), "/upgrade_to_enterprise/allowed", "")
	require.Error(t, err)
	require.Equal(t, http.StatusNotImplemented, resp.StatusCode)

	resp, err = th.Client.DoAPIPost(context.Background(), "/upgrade_to_enterprise", "")
	require.Error(t, err)
	require.Equal(t, http.StatusForbidden, resp.StatusCode)
}
