with src as (
    select
        cast(event_date as date) as event_date,
        coalesce(nullif(country, ''), 'UNKNOWN') as country,
        upper(platform) as platform,

        user_id,

        cast(match_start_count as int64) as match_start_count,
        cast(match_end_count as int64) as match_end_count,
        cast(victory_count as int64) as victory_count,
        cast(defeat_count as int64) as defeat_count,
        cast(server_connection_error as int64) as server_connection_error,

        cast(iap_revenue as float64) as iap_revenue,
        cast(ad_revenue as float64) as ad_revenue
    from {{ source('raw', 'user_daily_metrics_raw') }}
),

daily as (
    select
        event_date,
        country,
        platform,

        count(distinct user_id) as dau,

        sum(iap_revenue) as total_iap_revenue,
        sum(ad_revenue) as total_ad_revenue,

        safe_divide(
            sum(iap_revenue) + sum(ad_revenue),
            count(distinct user_id)
        ) as arpdau,

        sum(match_start_count) as matches_started,
        safe_divide(sum(match_start_count), count(distinct user_id)) as match_per_dau,

        safe_divide(sum(victory_count), nullif(sum(match_end_count), 0)) as win_ratio,
        safe_divide(sum(defeat_count), nullif(sum(match_end_count), 0)) as defeat_ratio,

        safe_divide(sum(server_connection_error), count(distinct user_id)) as server_error_per_dau
    from src
    group by 1,2,3
)

select * from daily
