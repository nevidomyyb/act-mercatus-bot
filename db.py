import sqlalchemy as db

# query = (
#     act_user
#     .join(user_papers, act_user.c.user_id == user_papers.c.user_id)
#     .join(paper, user_papers.c.paper_id == paper.c.paper_id)
#     .select()
#     .with_only_columns(
#         act_user.c.user_id.label('user_id'),
#         act_user.c.telegram_user,
#         paper.c.paper_id,
#         paper.c.name_paper,
#         paper.c.last_price
#     )
# )

# result = connection.execute(query)
# for row in result.fetchall():
#     print(row)