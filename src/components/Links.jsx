export default function Links() {
    const links = [
        {
            id: 1,
            link: 'linkedin.com',
            timestamp: 'a minute ago',
            author: {
                username: 'maciej',
            },
        },
        {
            id: 2,
            link: 'instragram.com',
            timestamp: 'a 2 minutes ago',
            author: {
                username: 'maciej',
            },
        },
    ]



    return (
        <>
            {links.length === 0 ?
                <p>No links</p>
                :
                links.map(link => {
                    return (
                        <p key={link.id}>
                            <b>{link.author.username}</b> &mdash; {link.timestamp}
                            <br />
                            {link.link}
                        </p>
                    );
                })}
        </>
    )
}