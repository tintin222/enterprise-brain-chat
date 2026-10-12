// Copyright (c) 2015-present Mattermost, Inc. All Rights Reserved.
// See LICENSE.txt for license information.

import React from 'react';

import ExternalLink from 'components/external_link';

import './team_edition.scss';
export interface TeamEditionProps {
    openEELicenseModal: () => void;
}

// Enterprise Brain: what this server runs and under which licence, in place of Mattermost's edition panel.
// Note: like the original, these strings are not localised because they describe licences.
const TeamEdition: React.FC<TeamEditionProps> = () => {
    const title = 'Enterprise Brain';
    return (
        <div className='TeamEditionLeftPanel'>
            <div className='TeamEditionLeftPanel__Header'>
                <div className='TeamEditionLeftPanel__Title'>{title}</div>
            </div>
            <div className='TeamEditionLeftPanel__LicenseNotices'>
                <p>{'This server runs Enterprise Brain chat, a build of Mattermost Team Edition without the user limit. It needs no licence key, and it cannot be upgraded to Mattermost Enterprise Edition.'}</p>
                <p>
                    {'Its source code is published under the GNU AGPL v3 at '}
                    <ExternalLink
                        location='license_settings'
                        href='https://github.com/tintin222/enterprise-brain-chat'
                    >
                        {'github.com/tintin222/enterprise-brain-chat'}
                    </ExternalLink>
                    {'. Mattermost is a trademark of Mattermost, Inc.'}
                </p>
                <p>{'See NOTICE.txt for information about open source software used in the system.'}</p>
            </div>
        </div>
    );
};

export default TeamEdition;
