from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date


class social_model(BaseModel):
    """
    Pydantic model for social media data collection.
    Used to standardize data structure across different social media platforms.
    """
    m_weblink: List[str] = Field(default_factory=list)
    m_username: str =None
    m_network: str =None
    m_real_name: str = None
    m_total_posts: str = None
    m_followers : List[str] = None
    m_following : List[str] = None
    m_total_followers : str = None
    m_total_following : str = None
    m_bio : str = None
    m_content: Optional[str] = None
    m_content_type: List[str] = Field(default_factory=list)
    m_channel_url: Optional[str] = None
    m_platform: str
    m_post_comments: Optional[str] = None
    m_post_likes: Optional[str] = None
    m_post_shares: Optional[str] = None
    m_post_comments_count: Optional[str] = None
    m_post_views: Optional[str] = None
    m_views: Optional[str] = None
    m_comment_count: Optional[str] = None
    m_likes: Optional[str] = None
    m_retweets: Optional[str] = None
    m_commenters: List[str] = Field(default_factory=list)
    m_mutual_usernames: List[str] = Field(default_factory=list)