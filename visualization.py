import plotly.graph_objects as go
import plotly.express as px


def plot_clusters(df):
    # Figure 1: Cluster Scatter Plot
    fig_clusters = go.Figure()
    clusters = df['Cluster'].unique()

    for cluster in clusters:
        cluster_data = df[df['Cluster'] == cluster]
        fig_clusters.add_trace(go.Scatter(
            x=cluster_data['Age'],
            y=cluster_data['SpendingScore'],
            mode='markers',
            name=f'Cluster {cluster}',
            marker=dict(size=8, opacity=0.8)
        ))

    fig_clusters.update_layout(
        title='Customer Segmentation - Clusters',
        xaxis_title='Age',
        yaxis_title='Spending Score',
        template='plotly_white'
    )

    # Figure 2: Histogram of Age
    fig_hist = go.Figure(go.Histogram(
        x=df['Age'],
        nbinsx=20,
        marker_color='#636EFA',
        opacity=0.95
    ))

    fig_hist.update_layout(
        title='Histogram of Age',
        xaxis_title='Age',
        yaxis_title='Count',
        bargap=0.1,
        template='plotly_white'
    )
    fig_anual_spend = go.Figure(go.Scatter(
        x=df['Income'],
        y=df['SpendingScore'],
        mode='markers',
        marker=dict(size=8, opacity=0.8, color='#EF553B')
    ))

    fig_anual_spend.update_layout(
        title='Annual Income vs. Spending Score',
        xaxis_title='Annual Income',
        yaxis_title='Spending Score',
        template='plotly_white'
    )
    fig_anual_spend = go.Figure(go.Scatter(
        x=df['Income'],
        y=df['SpendingScore'],
        mode='markers',
        marker=dict(size=8, opacity=0.8, color='#EF553B')
    ))

    fig_anual_spend.update_layout(
        title='Annual Income vs. Spending Score',
        xaxis_title='Annual Income',
        yaxis_title='SpendingScore',
        template='plotly_white'
    )
    clusters = df['Cluster'].unique()

    for cluster in clusters:
        cluster_data = df[df['Cluster'] == cluster]
        fig_clusters.add_trace(go.Scatter(
            x=cluster_data['Income'],
            y=cluster_data['SpendingScore'],
            mode='markers',
            name=f'Cluster {cluster}',
            marker=dict(size=8, opacity=0.8)
        ))

    fig_clusters.update_layout(
        title='Customer Segmentation - Clusters',
        xaxis_title='income',
        yaxis_title='Spending Score',
        template='plotly_white'
    )
    fig_color = px.scatter(df, x="Income", y="SpendingScore",
                     title="Age vs Spending Score (1-100)", color_continuous_scale="Inferno")
    fig_color.update_layout(xaxis_title="Age (Years)", yaxis_title="Spending Score")
    # st.plotly_chart(fig)
    # fig_color = go.Figure(go.Scatter(
    #     x=df["Income"],
    #     y=df["SpendingScore"],
    #     mode='markers',
    #     marker=dict(
    #         size=8,
    #         color=df["cluster"],  # Directly use cluster labels for coloring
    #         colorscale='viridis',
    #         colorbar=dict(title="Cluster"),
    #         opacity=0.8
    #     )
    # ))
    #
    # fig_color.update_layout(
    #     title="Annual Income vs Spending Score (1-100)",
    #     xaxis_title="Income",
    #     yaxis_title="Spending Score (1-100)",
    #     template='plotly_white'
    # )
    # st.plotly_chart(fig_color)
    # Return both figures clearly
    return fig_clusters, fig_hist ,fig_anual_spend,fig_color


# import matplotlib.pyplot as plt
# import plotly.graph_objects as go
# import streamlit as st
#
# def plot_clusters(df):
#     # plt.figure(figsize=(8, 6))
#     # clusters = df['Cluster'].unique()
#     #
#     # for cluster in clusters:
#     #     cluster_data = df[df['Cluster'] == cluster]
#     #     plt.scatter(cluster_data['Age'], cluster_data['SpendingScore'], label=f'Cluster {cluster}')
#     #
#     # plt.xlabel('Age')
#     # plt.ylabel('Spending Score')
#     # plt.legend()
#     # plt.title('Customer Segmentation - Clusters')
#     # plt.grid(True)
#
#     clusters = df['Cluster'].unique()
#     fig2 = go.Figure()
#     # Loop through each cluster and plot points
#     for cluster in clusters:
#         cluster_data = df[df['Cluster'] == cluster]
#
#         fig2.add_trace(go.Scatter(
#             x=cluster_data['Age'],
#             y=cluster_data['SpendingScore'],
#             mode='markers',
#             name=f'Cluster {cluster}',
#             marker=dict(size=8, opacity=0.8)
#         ))
#
#     # Update figure layout
#     fig2.update_layout(
#         title='Customer Segmentation - Clusters',
#         xaxis_title='Age',
#         yaxis_title='Spending Score',
#         template='plotly_white'
#     )
#
#     st.plotly_chart(fig2)
#     # Directly specify your column (e.g., 'likes')
#     fig = go.Figure(go.Histogram(
#         x=df['Age'],
#         nbinsx=20,
#         marker_color='#636EFA',
#         opacity=0.95
#     ))
#
#     # Update plot layout
#     fig.update_layout(
#         title='Histogram of Likes',
#         xaxis_title='Age',
#         yaxis_title='Count',
#         bargap=0.1
#     )
#
#     # Display histogram
#     st.plotly_chart(fig)
#
#     return fig,fig2

