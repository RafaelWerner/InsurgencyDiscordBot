from db.migration_manager import Migration

class UpdateServerMessagesTask(Migration):
    id = 20241224130015

    def sql(self):
        return """
                UPDATE task
                SET
                interval = 300,
                data = '[
                    "Bem-vindo ao servidor KPX! Lembre-se de seguir as regras e respeitar todos os jogadores.",
                    "Anti-Jogo >>> Denunciem no Discord <<<",
                    "Entre em nosso DISCORD: >>> discord.me/gackpx <<<",
                    "Regra 1: Respeite todos os jogadores, qualquer desrespeito será punido com ban permanente.",
                    "Regra 2: Comunique-se com o time, trabalho em equipe é essencial.",
                    "Regra 4: Espere o time para capturar ou destruir o objetivo, na dúvida? Pergunte!",
                    "Regra 3: NÃO RUSHE NO OBJETIVO, ao morrer você prejudica o time, que terá de lidar com os bots que foram incluidos para você.",
                    "Regra 5: Evite Flashbang e Smoke, os bots conseguem ver através da fumaça e não são tão afetados pela flash, acaba só atrapalhando os colegas.",
                    "Rules: Respect all players. Comunicate with your team. Wait for the team to capture or destroy the objective. Avoid Flashbang and Smoke.",
                    "Regla: Respeta a todos los jugadores. Comunícate con tu equipo. Espera a que el equipo capture o destruya el objetivo. Evita Flashbang y Smoke."
                ]'
                WHERE kind = 'server_messages';
            """
