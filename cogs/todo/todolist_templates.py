import discord

def help_template():
    emb = discord.Embed(title="To-do List", colour=0xe67e22)

    emb.add_field(name = "**Adicionar tarefa** 📙", value = "!todo add <tarefa>")
    emb.add_field(name = "**Remover tarefa** ❌", value = "!todo del <num>")
    emb.add_field(name = "**Completar tarefa** ✅", value = "!todo done <num>")
    emb.add_field(name = "**Tarefas concluídas** 📈", value = "!todo stats")

    return emb

def list_template(name, dic : dict):
    emb = discord.Embed(title="{}'s list".format(name), colour=0xe67e22)

    for i, task in enumerate(dic.values()):
        emb.add_field(name = "Task {}".format(i+1), value = task)

    return emb